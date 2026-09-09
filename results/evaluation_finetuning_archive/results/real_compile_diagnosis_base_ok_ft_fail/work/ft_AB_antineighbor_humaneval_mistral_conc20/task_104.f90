program main
  implicit none
  integer, parameter :: x_len = 4
  integer, dimension(x_len) :: x
  integer :: i
  integer :: result_len
  integer, dimension(:), allocatable :: result

  ! Hardcoded input as per example
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, dimension(:), allocatable :: res
    integer :: i, j, k, len
    integer :: temp
    logical :: has_even

    ! Initialize result array
    allocate(res(x_len))
    len = 0

    ! Filter elements that don't contain even digits
    do i = 1, x_len
      has_even = .false.
      temp = x(i)
      do while (temp > 0)
        if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. &
            mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. &
            mod(temp, 10) == 8) then
          has_even = .true.
          exit
        end if
        temp = temp / 10
      end do
      if (.not. has_even) then
        len = len + 1
        res(len) = x(i)
      end if
    end do

    ! Sort the result array
    do i = 1, len - 1
      do j = i + 1, len
        if (res(i) > res(j)) then
          temp = res(i)
          res(i) = res(j)
          res(j) = temp
        end if
      end do
    end do

    ! Resize the result array to the correct size
    allocate(res(len))

  end function unique_digits

end program main