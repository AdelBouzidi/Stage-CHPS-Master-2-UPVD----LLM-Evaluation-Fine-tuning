program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: n, i, j, k, len

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Call the function
  call unique_digits(x_len, x, result, n)

  ! Output result
  print *, n
  print *, result

contains

  subroutine unique_digits(x_len, x, result, n)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, intent(out) :: result(:)
    integer, intent(out) :: n
    integer :: i, j, k, len
    logical :: has_even

    n = 0
    do i = 1, x_len
      has_even = .false.
      do j = 1, len(x(i))
        if (mod(x(i), 10) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        n = n + 1
      end if
    end do

    allocate(result(n))
    k = 0
    do i = 1, x_len
      has_even = .false.
      do j = 1, len(x(i))
        if (mod(x(i), 10) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        k = k + 1
        result(k) = x(i)
      end if
    end do

    result = sort(result)
  end subroutine unique_digits

  function sort(arr) result(sorted)
    implicit none
    integer, intent(in) :: arr(:)
    integer :: sorted(:)
    integer :: i, j, temp
    sorted = arr
    do i = 1, size(sorted) - 1
      do j = i + 1, size(sorted)
        if (sorted(j) < sorted(i)) then
          temp = sorted(i)
          sorted(i) = sorted(j)
          sorted(j) = temp
        end if
      end do
    end do
  end function sort

end program main