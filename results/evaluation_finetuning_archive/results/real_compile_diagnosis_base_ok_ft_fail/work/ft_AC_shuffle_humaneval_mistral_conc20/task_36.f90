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
    integer, intent(in) :: n
    integer :: i, count
    character(len=10) :: num_str

    count = 0
    do i = 1, n-1
      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
        num_str = i_char(i)
        if (index(num_str, '7') > 0) then
          count = count + 1
        end if
      end if
    end do
    fizz_buzz = count
  end function fizz_buzz

  character(len=10) function i_char(i)
    integer, intent(in) :: i
    write(i_char, '(I0)') i
  end function i_char

end program fizz_buzz