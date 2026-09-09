program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, n

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, j, n, temp
    logical :: has_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0

    ! Check each element
    do i = 1, x_len
      has_even = .false.
      temp = x(i)
      do while (temp > 0)
        if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
          has_even = .true.
          exit
        end if
        temp = temp / 10
      end do
      if (.not. has_even) then
        n = n + 1
        res(n) = x(i)
      end if
    end do

    ! Sort the result
    call sort_array(res, n)

  end function unique_digits

  subroutine sort_array(arr, n)
    implicit none
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    do i = 1, n-1
      do j = 1, n-i
        if (arr(j) > arr(j+1)) then
          temp = arr(j)
          arr(j) = arr(j+1)
          arr(j+1) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program main