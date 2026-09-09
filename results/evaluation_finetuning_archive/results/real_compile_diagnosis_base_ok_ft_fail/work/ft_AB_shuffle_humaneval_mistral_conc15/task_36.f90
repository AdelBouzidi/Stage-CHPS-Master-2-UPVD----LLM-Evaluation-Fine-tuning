program fizz_buzz
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate the result
  result = fizz_buzz(n)

  ! Output the result
  print *, result

contains

  integer function fizz_buzz(n)
    implicit none
    integer, intent(in) :: n
    integer :: i, temp

    fizz_buzz = 0
    do i = 1, n-1
      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
        temp = i
        do while (temp > 0)
          if (mod(temp, 10) == 7) then
            fizz_buzz = fizz_buzz + 1
          end if
          temp = temp / 10
        end do
      end if
    end do
  end function fizz_buzz

end program fizz_buzz