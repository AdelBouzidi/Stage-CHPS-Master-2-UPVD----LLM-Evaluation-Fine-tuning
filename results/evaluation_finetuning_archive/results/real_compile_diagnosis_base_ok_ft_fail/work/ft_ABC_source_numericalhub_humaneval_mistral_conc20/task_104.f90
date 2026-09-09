program test_unique_digits
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b), dimension(:), allocatable :: x
  integer(i4b), dimension(:), allocatable :: result
  integer(i4b) :: x_len

  ! Read input
  read(*,*) x_len
  read(*,*) x

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer(i4b), intent(in) :: x_len
    integer(i4b), intent(in) :: x(:)
    integer(i4b), allocatable :: res(:)
    integer(i4b) :: i, n
    integer(i4b), allocatable :: temp(:)
    logical :: has_even
    integer(i4b) :: digit

    n = 0
    do i = 1, x_len
      has_even = .false.
      do
        digit = mod(x(i), 10)
        if (digit /= 0) then
          if (mod(digit, 2) == 0) then
            has_even = .true.
            exit
          end if
        end if
        x(i) = x(i) / 10
        if (x(i) == 0) exit
      end do
      if (.not. has_even) then
        n = n + 1
        temp(n) = x(i)
      end if
    end do

    allocate(res(n))
    res = temp
    call sort(res)
  end function unique_digits

  subroutine sort(arr)
    implicit none
    integer(i4b), intent(inout) :: arr(:)
    integer(i4b) :: i, j, temp
    do i = size(arr) - 1, 1, -1
      do j = 1, i
        if (arr(j) > arr(j+1)) then
          temp = arr(j)
          arr(j) = arr(j+1)
          arr(j+1) = temp
        end if
      end do
    end do
  end subroutine sort

end program test_unique_digits