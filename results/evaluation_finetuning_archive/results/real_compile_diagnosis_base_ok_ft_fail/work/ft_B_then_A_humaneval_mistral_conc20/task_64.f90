program vowels_count_demo
          implicit none
          character(len=*) :: input_string
          integer :: count
          integer :: i
          character(len=1) :: char

          read(*, '(A)') input_string

          count = 0
          do i = 1, len(input_string)
            char = input_string(i:i)
            select case (lowercase(char))
            case ('a', 'e', 'i', 'o', 'u')
              count = count + 1
            case ('y')
              if (i == len(input_string)) then
                count = count + 1
              end if
            end select
          end do

          print *, count

        end program vowels_count_demo